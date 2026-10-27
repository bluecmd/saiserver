use serde::Serialize;
use std::{
    collections::{BTreeMap, VecDeque},
    time::{Duration, Instant},
};

pub const COUNTERS: &[&str] = &[
    "in_octets",
    "out_octets",
    "in_packets",
    "out_packets",
    "in_errors",
    "out_errors",
    "in_discards",
    "out_discards",
];
pub const HISTORY_LIMIT: usize = 120;
#[derive(Clone, Debug, Default, Serialize)]
pub struct RateSample {
    pub in_bps: Option<f64>,
    pub out_bps: Option<f64>,
    pub interval_seconds: Option<f64>,
    pub notes: Vec<String>,
}
pub struct Rates {
    previous: Option<(Instant, BTreeMap<String, u64>)>,
    pub history: VecDeque<RateSample>,
    max_gap: Duration,
}
impl Rates {
    pub fn new(interval: Duration) -> Self {
        Self {
            previous: None,
            history: VecDeque::new(),
            max_gap: interval.saturating_mul(4),
        }
    }
    fn push(&mut self, sample: RateSample) -> RateSample {
        if self.history.len() == HISTORY_LIMIT {
            self.history.pop_front();
        }
        self.history.push_back(sample.clone());
        sample
    }
    /// A different port is a different history, not a continuation of traffic.
    pub fn clear(&mut self) {
        self.previous = None;
        self.history.clear();
    }
    /// Disconnect/error invalidates the baseline; the next connection starts cold.
    pub fn disconnected(&mut self, reason: &str) -> RateSample {
        self.previous = None;
        self.push(RateSample {
            notes: vec![format!("counter gap / reconnect: {reason}; baseline reset")],
            ..RateSample::default()
        })
    }
    pub fn sample(&mut self, now: Instant, counters: &BTreeMap<String, u64>) -> RateSample {
        let mut sample = RateSample::default();
        for name in COUNTERS.iter().filter(|n| !counters.contains_key(**n)) {
            sample.notes.push(format!("{name} unavailable (not zero)"));
        }
        if let Some((when, previous)) = &self.previous {
            let dt = now.saturating_duration_since(*when);
            if dt.is_zero() || dt > self.max_gap {
                sample
                    .notes
                    .push("invalid/stale interval; baseline reset".into());
            } else {
                sample.interval_seconds = Some(dt.as_secs_f64());
                for (name, rate) in [
                    ("in_octets", &mut sample.in_bps),
                    ("out_octets", &mut sample.out_bps),
                ] {
                    match (previous.get(name), counters.get(name)) {
                        (Some(&old), Some(&new)) => {
                            let delta = if new >= old {
                                Some(new - old)
                            } else if old >= u64::MAX - u32::MAX as u64 && new <= u32::MAX as u64 {
                                sample.notes.push(format!("{name}: u64 wrap"));
                                Some(new.wrapping_sub(old))
                            } else {
                                sample
                                    .notes
                                    .push(format!("{name}: counter reset; baseline reset"));
                                None
                            };
                            *rate = delta.map(|d| d as f64 * 8.0 / dt.as_secs_f64());
                        }
                        _ => sample
                            .notes
                            .push(format!("{name}: missing baseline/sample")),
                    }
                }
            }
        } else {
            sample
                .notes
                .push("initial sample; rates need two successful observations".into());
        }
        // Missing fields are deliberately absent from the next baseline too.
        self.previous = Some((now, counters.clone()));
        self.push(sample)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn map(a: u64, b: u64) -> BTreeMap<String, u64> {
        BTreeMap::from([("in_octets".into(), a), ("out_octets".into(), b)])
    }
    #[test]
    fn actual_intervals_reset_missing_wrap_and_reconnect() {
        let t = Instant::now();
        let mut r = Rates::new(Duration::from_secs(1));
        assert!(r.sample(t, &map(100, 200)).in_bps.is_none());
        let s = r.sample(t + Duration::from_millis(1500), &map(400, 800));
        assert_eq!(s.in_bps, Some(1600.0));
        assert_eq!(s.out_bps, Some(3200.0));
        let s = r.sample(t + Duration::from_secs(2), &map(1, 2));
        assert!(s.in_bps.is_none());
        assert!(s.notes.iter().any(|s| s.contains("reset")));
        assert_eq!(
            r.sample(t + Duration::from_secs(3), &map(101, 202)).in_bps,
            Some(800.0)
        );
        r.sample(t + Duration::from_secs(4), &BTreeMap::new());
        assert!(r
            .sample(t + Duration::from_secs(5), &map(201, 302))
            .in_bps
            .is_none());
        r.disconnected("timeout");
        assert!(r
            .sample(t + Duration::from_secs(6), &map(301, 402))
            .in_bps
            .is_none());
        r.disconnected("new selection");
        r.sample(t + Duration::from_secs(7), &map(u64::MAX - 9, u64::MAX - 4));
        let s = r.sample(t + Duration::from_secs(8), &map(10, 5));
        assert_eq!(s.in_bps, Some(160.0));
        assert_eq!(s.out_bps, Some(80.0));
        assert!(s.notes.iter().any(|s| s.contains("wrap")));
    }
    #[test]
    fn stale_zero_intervals_and_bounded_history() {
        let t = Instant::now();
        let mut r = Rates::new(Duration::from_secs(1));
        r.sample(t, &map(0, 0));
        assert!(r.sample(t, &map(1, 1)).in_bps.is_none());
        assert!(r
            .sample(t + Duration::from_secs(10), &map(10, 10))
            .in_bps
            .is_none());
        for i in 0..1000 {
            r.sample(t + Duration::from_secs(i + 11), &map(i, i));
        }
        assert_eq!(r.history.len(), HISTORY_LIMIT);
    }
}

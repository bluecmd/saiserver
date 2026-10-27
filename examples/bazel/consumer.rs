use std::io::Cursor;
use thrift::protocol::{TBinaryInputProtocol, TBinaryOutputProtocol, TSerializable};

#[test]
fn public_bindings_serialize_with_the_exported_runtime() {
    let inventory = sai_tui_rpc::Inventory {
        objects: Some(vec![]),
        warnings: Some(vec!["downstream-wire-smoke".into()]),
    };
    let mut bytes = Vec::new();
    inventory
        .write_to_out_protocol(&mut TBinaryOutputProtocol::new(&mut bytes, true))
        .unwrap();
    let decoded = sai_tui_rpc::Inventory::read_from_in_protocol(
        &mut TBinaryInputProtocol::new(Cursor::new(&bytes), true),
    )
    .unwrap();
    assert_eq!(decoded, inventory);

    // The client crate uses the same runtime identity, with its Cargo-compatible
    // nested generated module. Its types also decode the independently generated
    // crate's actual bytes.
    let client_decoded = sai_tui::sai_tui::Inventory::read_from_in_protocol(
        &mut TBinaryInputProtocol::new(Cursor::new(&bytes), true),
    )
    .unwrap();
    assert_eq!(client_decoded.warnings, inventory.warnings);
}

#[test]
fn downstream_protocols_construct_a_generated_service_client() {
    let client = sai_tui_rpc::SaiTuiSyncClient::new(
        TBinaryInputProtocol::new(Cursor::new(Vec::<u8>::new()), true),
        TBinaryOutputProtocol::new(Vec::<u8>::new(), true),
    );
    fn accepts_service_client(_: &impl sai_tui_rpc::TSaiTuiSyncClient) {}
    accepts_service_client(&client);
}

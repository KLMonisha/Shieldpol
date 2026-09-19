from app.token_vault import TokenVault


def test_token_vault_restores_values():
    vault = TokenVault()

    vault.store(
        "[PAN_1]",
        "ABCDE1234F",
    )

    vault.store(
        "[PHONE_1]",
        "+91 9876543210",
    )

    response = (
        "Customer [PAN_1] can be contacted at "
        "[PHONE_1]."
    )

    restored = vault.restore(response)

    assert "ABCDE1234F" in restored
    assert "+91 9876543210" in restored
    assert "[PAN_1]" not in restored
    assert "[PHONE_1]" not in restored


def test_vault_can_be_cleared():
    vault = TokenVault()

    vault.store("[PAN_1]", "ABCDE1234F")

    assert len(vault) == 1

    vault.clear()

    assert len(vault) == 0
"""Check that CycleCity can read its alert webhook from Key Vault, without showing it.

Run it from cyclecity/ once task 11 has made pyproject.toml:

    KEY_VAULT_URL=$(terraform -chdir=infra output -raw key_vault_uri) uv run python -m cyclecity.check_secret
"""

SECRET_NAME = "alert-webhook-url"


def main() -> None:
    """Read the secret with your own sign-in and print facts about it, never its value.

    - Take the vault address from the KEY_VAULT_URL environment variable. If it is missing,
      stop with a clear message instead of a stack trace.
    - Sign in with DefaultAzureCredential (it uses your az login) and make a SecretClient
      for that vault.
    - Get SECRET_NAME. Print its name, properties.enabled, properties.updated_on and the
      length of its value.
    - Never print, log or write the value itself.
    """
    raise NotImplementedError("TODO(task 11): read the secret as the docstring says")


if __name__ == "__main__":
    main()

## Testing

    pip install -e '.[dev]'
    pre-commit autoupdate
    pre-commit install
    pre-commit run --all-files
    tox

On a macos machine:

    tests/tox_mac.sh

## Releasing

    TBD

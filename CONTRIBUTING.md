## Linting & Testing

    pip install -e '.[dev]'
    pre-commit autoupdate
    pre-commit install
    pre-commit run --all-files
    tox

`tox` uses by default the installed `protoc` compiler. The gh repo `test` workflow considers `protoc` in various versions (`3.20.3`, `21.12`, `25.x`).
Contributors using a macOS workstation shall have a look at `tests/tox_mac.sh` to test against `protobuf`, `protobuf@21` and `protobuf@3` bottles.
 
## Releasing

If dev branch `test` workflow succeed, a new version can be released.

1. Version

    Use `bumpver` on dev branches (fist, with `--dry`)
    
    Breaking changes:
    
        bumpver update --major --dry
    
    Additional features:
    
        bumpver update --minor --dry
    
    Other:
    
        bumpver update --patch --dry

2. Merge

   To `master`

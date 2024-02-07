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

    Use `bumpver` on dev branches. First, with `--dry`, then without :)
    
    Breaking changes:
    
        bumpver update --major --dry
    
    Additional features:
    
        bumpver update --minor --dry
    
    Other:
    
        bumpver update --patch --dry

2. Merge

   To `main`

3. Publish

   Publishing to PyPi is done through the creation of a release in the [Github UI](https://github.com/decitre/python-proto-topy/releases):
   - "Draft a new release"
   - Choose the tag created in step 1
   - Use it to name the release
   - Add the changes to the description field
   - "Publish release"
   - Check the `release` [action](https://github.com/decitre/python-proto-topy/actions/workflows/release.yml)

4. Install published package

   In a dedicated `venv`, do:

         pip install proto_topy==<new-version>
         python -c "import proto_topy as pt; print(pt.__version__, pt.ProtoCollection().compiler_version())"

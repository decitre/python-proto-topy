PROTOC_BOTTLES="protobuf@3 protobuf@21 protobuf"
YELLOW='\033[33m'
NC='\033[0m'

brew install $PROTOC_BOTTLES
brew unlink $PROTOC_BOTTLES
PATHBAK=$PATH

for bottle in $PROTOC_BOTTLES; do
  printf "${YELLOW}Use $bottle${NC}\n"
  brew link --overwrite --force $bottle
  PATH="/usr/local/opt/$bottle/bin:$PATHBAK"
  protoc --version
  tox
  [[ $? -ne 0 ]] && break
  brew unlink $bottle
done

brew link --overwrite protobuf

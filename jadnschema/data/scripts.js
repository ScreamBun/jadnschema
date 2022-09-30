function hash2id(hash) {
  if (hash.startsWith("#")) {
    return hash.substring(1);
  }
  return hash
}

var prevHash = hash2id(location.hash);

function locationHashChanged(e) {
  var currHash = hash2id(location.hash);
  if (prevHash != currHash) {
    console.log(prevHash, currHash);
    if (prevHash) {
      document.getElementById(prevHash).classList.remove('hash');
    }
    document.getElementById(currHash).classList.add('hash');
    prevHash = currHash;
  }
}

window.onhashchange = locationHashChanged;

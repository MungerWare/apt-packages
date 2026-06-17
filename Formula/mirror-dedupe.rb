class MirrorDedupe < Formula
  desc "Pool-based content-addressable Debian/Ubuntu mirror syncing with hardlink deduplication"
  homepage "https://github.com/Munger/mirror-dedupe"
  url "https://github.com/Munger/mirror-dedupe/archive/refs/tags/v0.2.11.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3.14"

  def install
    bin.install "mirror-dedupe"
  end
end

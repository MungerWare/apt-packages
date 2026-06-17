class MikroCommon < Formula
  desc "Common libraries for Munger infrastructure tools"
  homepage "https://github.com/Munger/mikro-common"
  url "https://github.com/Munger/mikro-common/archive/refs/tags/v0.1.1.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  def install
    bin.install "mikro-common"
  end
end

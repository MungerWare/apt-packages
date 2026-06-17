class MikroDns < Formula
  desc "DNS management tool for Munger infrastructure"
  homepage "https://github.com/Munger/mikro-dns"
  url "https://github.com/Munger/mikro-dns/archive/refs/tags/v0.1.1.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  def install
    bin.install "mikro-dns"
  end
end

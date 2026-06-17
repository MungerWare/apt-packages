class MungerPxeboot < Formula
  desc "PXE boot server configuration for Munger infrastructure"
  homepage "https://github.com/Munger/munger-pxeboot"
  url "https://github.com/Munger/munger-pxeboot/archive/refs/tags/v1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  def install
    bin.install "munger-pxeboot"
  end
end

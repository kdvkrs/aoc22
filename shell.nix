{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.pypy3
    pkgs.python310Packages.requests
    pkgs.python310Packages.progressbar2
    pkgs.python310
  ];
}

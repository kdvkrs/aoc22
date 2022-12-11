{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python310Packages.requests
    pkgs.python310Packages.progressbar2

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}

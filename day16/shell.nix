{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python310Packages.cvxpy
    pkgs.python310Packages.numpy

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}

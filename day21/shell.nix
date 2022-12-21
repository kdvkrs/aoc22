{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.hello

    # keep this line if you use bash
    pkgs.bashInteractive
    pkgs.python310
    pkgs.python310Packages.z3
    pkgs.z3
  ];
}

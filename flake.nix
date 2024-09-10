{
  description = "For bootstrapping development environment with dependencies";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05-small";
    systems.url = "github:nix-systems/default";
  };

  outputs = inputs: let
    pyproject = {
      version = 312;
      dependencies = [
        "fastapi"
        "pydantic"
        "sqlalchemy"
      ];
    };

    inherit (builtins) toString;
    inherit (inputs.nixpkgs.lib) flatten map;
  in
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      systems = import inputs.systems;

      perSystem = {pkgs, ...}: let
        py = "python" + (toString pyproject.version);
      in {
        devShells.default = pkgs.mkShell {
          venvDir = ".venv";
          packages = flatten [
            pkgs.${py}
            pkgs."${py}Packages".venvShellHook
            (map (p: pkgs."${py}Packages".${p}) pyproject.dependencies)
          ];
        };
      };
    };
}

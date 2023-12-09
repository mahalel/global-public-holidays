{
  description = "Python dev environment";

  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/2c7f3c0fb7c08a0814627611d9d7d45ab6d75335"; # also valid: "nixpkgs"
  };

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      packages = forAllSystems({ pkgs }: {
        dockerImage = pkgs.dockerTools.buildImage {
          name = "global-public-holidays";
          config = { Cmd = ["python main.py"]; };
        };
      });
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default =
          let
          in
          pkgs.mkShell {
            # The Nix packages provided in the environment
            packages = [
              pkgs.python311Packages.python-lsp-server
              pkgs.python311Packages.plotly
              pkgs.python311Packages.pandas
              pkgs.python311Packages.packaging
              pkgs.python311Packages.pysnooper
              pkgs.python311Packages.geopy
              pkgs.python311Packages.openai
              pkgs.python311Packages.dash
              pkgs.python311
              pkgs.devbox
            ];
          };
      });
    };
}

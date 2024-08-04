{
  description = "Weed Scraper";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }: utils.lib.eachSystem ["x86_64-linux"] (system: let
    pkgs = import nixpkgs { system = system; };
  in rec {
    packages = {
      pythonEnv =
        pkgs.python3.withPackages (ps: with ps; [ webdriver-manager openpyxl pandas requests beautifulsoup4 websocket-client selenium ]);
    };

    devShell = pkgs.mkShell {
      buildInputs = [
        pkgs.chromium
        pkgs.undetected-chromedriver
        packages.pythonEnv
      ];

      shellHook = ''
        export PATH=${pkgs.chromium}/bin:${pkgs.undetected-chromedriver}/bin:$PATH
      '';
    };
  });
}

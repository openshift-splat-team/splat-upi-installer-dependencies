from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MultiArchBuildConfigTests(unittest.TestCase):
    def test_govc_containerfile_selects_verified_linux_amd64_and_arm64_artifacts(self):
        text = (ROOT / "images/govc/Containerfile").read_text()
        self.assertIn("ARG TARGETARCH", text)
        self.assertIn("amd64) govc_arch=x86_64", text)
        self.assertIn("arm64) govc_arch=arm64", text)
        self.assertIn('archive="govc_Linux_${govc_arch}.tar.gz"', text)
        self.assertIn("bd204fdc941ceb04681144189492c8959adb39f5f8de76a56fa4835809bfd2ad", text)
        self.assertIn("a88481fc5dd9b302f3674bed754c14459f0515b13becb72f1de9930c58ff5468", text)

    def test_pwsh_containerfile_selects_verified_linux_amd64_and_arm64_artifacts(self):
        text = (ROOT / "images/pwsh/Containerfile").read_text()
        self.assertIn("ARG TARGETARCH", text)
        self.assertIn("amd64) powershell_arch=x64", text)
        self.assertIn("arm64) powershell_arch=arm64", text)
        self.assertIn('archive="powershell-${POWERSHELL_VERSION}-linux-${powershell_arch}.tar.gz"', text)
        self.assertIn("34d2ed497f11d3c160a6a20abd635686458d7c5173fede7ad354bd73327fe89b", text)
        self.assertIn("c0b465bb60b4d8814682e7f4078006c3a118ec10cf98deb2143849ac18aa2e39", text)
        self.assertIn("VMware.PowerCLI", text)
        self.assertIn("13.2.1.22851661", text)
        self.assertIn("EPS", text)
        self.assertIn("azure-cli", text)
        self.assertIn("2.61.0.post20240516044921", text)
        self.assertIn("AS azure-cli-build", text)
        self.assertIn("gcc python3 python3-devel python3-pip", text)
        self.assertIn("COPY --from=azure-cli-build", text)
        self.assertIn("azure-cli-requirements.lock", text)
        self.assertIn("mysql flexible-server list --help", text)
        lock = (ROOT / "images/pwsh/azure-cli-requirements.lock").read_text()
        self.assertIn("azure-mgmt-rdbms==10.2.0b17", lock)
        self.assertNotIn("upgrade-strategy=eager", text)

    def test_github_workflow_builds_both_platforms_and_never_pushes_pull_requests(self):
        text = (ROOT / ".github/workflows/build-multiarch-images.yml").read_text()
        self.assertIn("linux/amd64,linux/arm64", text)
        self.assertIn("quay.io/ocp-splat/${{ matrix.image }}", text)
        self.assertIn("github.event_name == 'workflow_dispatch'", text)
        self.assertIn("docker/build-push-action", text)


if __name__ == "__main__":
    unittest.main()

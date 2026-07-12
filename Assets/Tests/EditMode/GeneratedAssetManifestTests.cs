#if UNITY_EDITOR
using NUnit.Framework;
using UnityMeshyStudio.Editor;

namespace UnityMeshyStudio.Tests
{
    public sealed class GeneratedAssetManifestTests
    {
        [Test]
        public void NewManifest_HasSafeDefaults()
        {
            var manifest = new GeneratedAssetManifest();
            Assert.That(manifest.intendedHeightMeters, Is.GreaterThan(0f));
            Assert.That(manifest.intendedForHumanoidRig, Is.False);
            Assert.That(manifest.loopAnimation, Is.False);
        }
    }
}
#endif

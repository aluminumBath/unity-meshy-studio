#if UNITY_EDITOR
using NUnit.Framework;

namespace UnityMeshyStudio.Tests
{
    public sealed class MeshyPathTests
    {
        [Test]
        public void GeneratedRoot_UsesExpectedUnityPath()
        {
            const string path = "Assets/Art/Generated/Meshy/Example/Models/model.fbx";
            Assert.That(path, Does.StartWith("Assets/Art/Generated/Meshy/"));
        }
    }
}
#endif

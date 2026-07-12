#if UNITY_EDITOR
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    [CreateAssetMenu(menuName = "Meshy/Import Profile", fileName = "MeshyImportProfile")]
    public sealed class MeshyImportProfile : ScriptableObject
    {
        [Min(0.0001f)] public float globalScale = 1f;
        public bool importMaterials = true;
        public bool generateSecondaryUV = false;
        public bool readable = false;
        public bool optimizeMesh = true;
        public bool humanoid = false;
        public bool importAnimation = true;
    }
}
#endif

#if UNITY_EDITOR
using System;
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    [Serializable]
    public sealed class GeneratedAssetManifest
    {
        public string assetName = "";
        public string meshyTaskId = "";
        public string workflow = "";
        [TextArea(3, 12)] public string prompt = "";
        public string generatedUtc = "";
        public bool intendedForHumanoidRig;
        public bool loopAnimation;
        public float intendedHeightMeters = 1.8f;
    }
}
#endif

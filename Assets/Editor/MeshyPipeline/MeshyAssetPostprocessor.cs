#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    public sealed class MeshyAssetPostprocessor : AssetPostprocessor
    {
        private const string GeneratedRoot = "Assets/Art/Generated/Meshy/";

        private void OnPreprocessModel()
        {
            if (!assetPath.StartsWith(GeneratedRoot, System.StringComparison.Ordinal))
                return;

            var importer = (ModelImporter)assetImporter;
            importer.importMaterials = true;
            importer.isReadable = false;
            importer.optimizeMeshPolygons = true;
            importer.optimizeMeshVertices = true;
            importer.importAnimation = true;
            importer.animationType = ModelImporterAnimationType.Generic;
            importer.avatarSetup = ModelImporterAvatarSetup.NoAvatar;

            // Humanoid must be enabled deliberately after avatar validation.
            Debug.Log($"Meshy import defaults applied to {assetPath}. Validate scale, rig, materials, and animation before production use.");
        }
    }
}
#endif

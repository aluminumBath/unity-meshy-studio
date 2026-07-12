#if UNITY_EDITOR
using System;
using UnityEditor;
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    public static class TextureHealthScanner
    {
        [MenuItem("Tools/Unity Meshy Studio/Scan Generated Textures")]
        public static void Scan()
        {
            var guids = AssetDatabase.FindAssets("t:Texture2D", new[] {"Assets/Art/Generated/Meshy"});
            var warnings = 0;
            foreach (var guid in guids)
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer == null) continue;

                var lower = path.ToLowerInvariant();
                if ((lower.Contains("normal") || lower.Contains("_n.")) &&
                    importer.textureType != TextureImporterType.NormalMap)
                {
                    Debug.LogWarning($"Possible normal map not imported as NormalMap: {path}");
                    warnings++;
                }
                if (importer.maxTextureSize > 4096)
                {
                    Debug.LogWarning($"Generated texture exceeds 4K import cap: {path}");
                    warnings++;
                }
            }
            Debug.Log($"Unity Meshy Studio texture scan complete. Warnings: {warnings}");
        }
    }
}
#endif

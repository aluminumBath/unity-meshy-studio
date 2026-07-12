#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    public static class PrefabHealthScanner
    {
        [MenuItem("Tools/Unity Meshy Studio/Scan Generated Prefabs")]
        public static void Scan()
        {
            var guids = AssetDatabase.FindAssets("t:Prefab", new[] {"Assets/Art/Generated/Meshy"});
            var warnings = 0;
            foreach (var guid in guids)
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var root = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                if (root == null) continue;
                if (root.GetComponentInChildren<Renderer>(true) == null)
                {
                    Debug.LogWarning($"Generated prefab has no Renderer: {path}");
                    warnings++;
                }
                if (root.GetComponentInChildren<Collider>(true) == null)
                {
                    Debug.LogWarning($"Generated prefab has no Collider; confirm this is intentional: {path}");
                    warnings++;
                }
            }
            Debug.Log($"Unity Meshy Studio prefab scan complete. Warnings: {warnings}");
        }
    }
}
#endif

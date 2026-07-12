#if UNITY_EDITOR
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UnityMeshyStudio.Editor
{
    public static class SceneHealthScanner
    {
        [MenuItem("Tools/Unity Meshy Studio/Scan Open Scenes")]
        public static void Scan()
        {
            var issues = new List<string>();
            for (var s = 0; s < SceneManager.sceneCount; s++)
            {
                var scene = SceneManager.GetSceneAt(s);
                if (!scene.isLoaded) continue;
                foreach (var root in scene.GetRootGameObjects())
                {
                    foreach (var component in root.GetComponentsInChildren<Component>(true))
                    {
                        if (component == null)
                            issues.Add($"{scene.name}: missing script beneath {root.name}");
                    }
                }
            }

            if (issues.Count == 0)
                Debug.Log("Unity Meshy Studio: no missing scripts found in open scenes.");
            else
                Debug.LogWarning("Unity Meshy Studio scene findings:\n" + string.Join("\n", issues));
        }
    }
}
#endif

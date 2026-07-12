#if UNITY_EDITOR
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace UnityMeshyStudio.Editor
{
    public sealed class MeshyValidationWindow : EditorWindow
    {
        private Object targetAsset;
        private Vector2 scroll;
        private readonly List<string> findings = new();

        [MenuItem("Tools/Meshy/Validate Generated Asset")]
        public static void Open() => GetWindow<MeshyValidationWindow>("Meshy Validator");

        private void OnGUI()
        {
            targetAsset = EditorGUILayout.ObjectField("Model or Prefab", targetAsset, typeof(Object), false);
            using (new EditorGUI.DisabledScope(targetAsset == null))
            {
                if (GUILayout.Button("Validate"))
                    ValidateTarget();
            }

            scroll = EditorGUILayout.BeginScrollView(scroll);
            foreach (var finding in findings)
                EditorGUILayout.HelpBox(finding, MessageType.Info);
            EditorGUILayout.EndScrollView();
        }

        private void ValidateTarget()
        {
            findings.Clear();
            var path = AssetDatabase.GetAssetPath(targetAsset);
            if (string.IsNullOrWhiteSpace(path))
            {
                findings.Add("The selected object is not a project asset.");
                return;
            }

            findings.Add($"Asset path: {path}");
            var importer = AssetImporter.GetAtPath(path) as ModelImporter;
            if (importer != null)
            {
                findings.Add($"Animation type: {importer.animationType}");
                findings.Add($"Global scale: {importer.globalScale}");
                findings.Add($"Readable: {importer.isReadable}");
                findings.Add($"Import materials: {importer.importMaterials}");
                if (importer.animationType == ModelImporterAnimationType.Human)
                    findings.Add("Humanoid selected: open Rig configuration and verify every required bone and the avatar pose.");
                else
                    findings.Add("Rig is not Humanoid. This is safer by default; change only after confirming compatibility.");
            }
            else
            {
                findings.Add("No ModelImporter found. Validate prefab references, colliders, LODGroup, materials, and Animator manually.");
            }
        }
    }
}
#endif

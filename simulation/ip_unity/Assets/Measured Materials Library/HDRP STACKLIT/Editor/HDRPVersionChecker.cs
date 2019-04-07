using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;
using System.Text.RegularExpressions;
using System;

[InitializeOnLoad]
public class HDRPVersionChecker
{

    private static string RegexFind(string regex, string content)
    {
        string result = "";
        var regx = new Regex(regex);
        var match = regx.Match(content);
        if(match.Success)
        {
            if(match.Groups.Count == 2)
            {
                result = match.Groups[1].ToString();
            }
        }
        return result;
    }


    static HDRPVersionChecker()
    {
        var TmpResultFile = Path.Combine(Application.temporaryCachePath, "unity.com.materialLibraryCheck.txt");
        if(File.Exists(TmpResultFile))
            return;

        var pathToManifest = Path.GetFullPath("Packages/Manifest.json");
        if(!File.Exists(pathToManifest))
        {
            Debug.LogError("Missing Packages/Manifest.json");
            return;
        }
        string manifestContent = File.ReadAllText(pathToManifest);
        
        var regexSearch = "\"dependencies\"\\s*:\\s*{([^}]+)";
        var dependenciesContent = RegexFind(regexSearch, manifestContent);

        if (dependenciesContent == "")
        {
            Debug.LogError("Packages/Manifest.json doesn't contain dependencies section");
            return;
        }
        
        regexSearch = "\"com\\.unity\\.render-pipelines\\.high-definition\":\\s*\"([0-9]+\\.[0-9]+\\.[0-9]+).*?\"";

        var hdrpVersion = RegexFind(regexSearch, dependenciesContent);

        if(hdrpVersion ==  "")
        {
            Debug.LogError("High Definition Render Pipeline is not installed, please install it by clicking on Windows/Package Manager.");
            return;
        }
        
        var version = new Version(hdrpVersion);
        var minimumVersion = new Version("4.9.0");
        if( version < minimumVersion)
        {
            Debug.LogError("High Definition Render Pipeline Outdated.  Please install version " + minimumVersion.ToString() + " or higher by clicking on Windows/Package Manager.");
            return;
        }

        File.Create(TmpResultFile);  
    }
}

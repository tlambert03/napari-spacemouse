"""Python mapping for the 3DconnexionClient framework.

(experiment... not at all working)
"""
import objc

ConnexionClient = objc.loadBundle(
    "ConnexionClient",
    globals(),
    objc.pathForFramework("3DconnexionClient.framework"),
)


functions = [
    ("SetConnexionHandlers", b"iiiii"),
]

objc.loadBundleFunctions(ConnexionClient, globals(), functions)

# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('utils.py', '.'),
        ('add_tools_to_db.py', '.'),
        ('auth_routes.py', '.'),
        ('auth_utils.py', '.'),
        ('connection_manager.py', '.'),
        ('create_sqlite_tables.py', '.'),
        ('db_utils.py', '.'),
        ('doc_endpoints.py', '.'),
        ('generic_utils.py', '.'),
        ('integration_routes.py', '.'),
        ('query_routes.py', '.'),
        ('report_data_manager.py', '.'),
        ('tool_code_utilities.py', '.'),
        ('agents/*.py', 'agents'),
        ('agents/clarifier/*.py', 'agents/clarifier'),
        ('agents/planner_executor/*.py', 'agents/planner_executor'),
        ('agents/planner_executor/tool_helpers/*.py', 'agents/planner_executor/tool_helpers'),
        ('agents/planner_executor/toolboxes/*.py', 'agents/planner_executor/toolboxes'),
        ('agents/planner_executor/toolboxes/data_fetching/*.py', 'agents/planner_executor/toolboxes/data_fetching'),
        ('agents/planner_executor/toolboxes/stats/*.py', 'agents/planner_executor/toolboxes/stats'),
    ],
    hiddenimports=[
        'defog', 'fastapi', 'httpx', 'numpy', 'pandas', 'pandasql', 'pyyaml', 'requests', 'scipy', 'sqlalchemy', 'sqlalchemy.ext.automap'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)

a.datas += Tree('out', prefix='out')

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    exclude_binaries=False,
    name='defog',
    debug=False,
    bootloader_ignore_signals=True,
    strip=False,
    upx=True,
    console=False,
    icon='logo512.icns'
)

app = BUNDLE(
    exe,
    name='defog.app',
    icon='logo512.icns',
    bundle_identifier=None,
    version='0.0.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'LSUIElement': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'My File Format',
                'CFBundleTypeIconFile': 'MyFileIcon.icns',
                'LSItemContentTypes': ['com.example.myformat'],
                'LSHandlerRank': 'Owner',
                'LSUIElement': False
            }
        ]
    },
)

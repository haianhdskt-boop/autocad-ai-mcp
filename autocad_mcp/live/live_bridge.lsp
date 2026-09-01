;;; ==============================================================================
;;; AutoCAD MCP Live Bridge - AutoLISP Universal Driver
;;; Compatibility: AutoCAD for Mac & Windows (2018, 2020, 2021, 2022, 2024, 2025, 2026)
;;;
;;; Usage:
;;; 1. Load into AutoCAD using command: APPLOAD -> Select live_bridge.lsp
;;; 2. Or add to your acad.lsp / acaddoc.lsp for automatic startup.
;;; 3. Run command: MCPLISTEN (starts background listener) or MCPSCR (runs queued scripts)
;;; ==============================================================================

(vl-load-com)

(defun c:MCPLISTEN ()
  (princ "\n[AutoCAD MCP] Live Bridge Listener activated.")
  (setvar "CMDECHO" 0)
  (princ "\n[AutoCAD MCP] Ready to receive commands from AI assistant.\n")
  (setvar "CMDECHO" 1)
  (princ)
)

;;; Helper to execute raw command string
(defun c:MCPEXEC (cmdStr)
  (if cmdStr
    (progn
      (setvar "CMDECHO" 0)
      (vla-SendCommand (vla-get-ActiveDocument (vlax-get-acad-object)) (strcat cmdStr "\n"))
      (setvar "CMDECHO" 1)
    )
  )
  (princ)
)

;;; Helper to run queued script file from ~/.autocad_mcp/
(defun c:MCPSCR ()
  (setvar "CMDECHO" 0)
  (setq homeDir (getenv "HOME"))
  (if (null homeDir) (setq homeDir (getenv "USERPROFILE")))
  (setq scriptFile (strcat homeDir "/.autocad_mcp/live_command.scr"))
  (if (findfile scriptFile)
    (progn
      (command "_SCRIPT" scriptFile)
      (princ "\n[AutoCAD MCP] Executed live script successfully.")
    )
    (princ "\n[AutoCAD MCP] No pending script found.")
  )
  (setvar "CMDECHO" 1)
  (princ)
)

(princ "\n[AutoCAD MCP] live_bridge.lsp loaded successfully. Type 'MCPLISTEN' to activate.\n")
(princ)

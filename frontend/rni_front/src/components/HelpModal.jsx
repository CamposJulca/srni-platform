// src/components/HelpModal.jsx
import React from "react";
import "../assets/help_modal.css";

export default function HelpModal({ open, title, children, onClose }) {
  if (!open) return null;

  return (
    <div className="hm-backdrop" onMouseDown={onClose}>
      <div className="hm-card" onMouseDown={(e) => e.stopPropagation()}>
        <div className="hm-header">
          <h3 className="hm-title">{title}</h3>
          <button className="hm-close" type="button" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="hm-body">{children}</div>

        <div className="hm-footer">
          <button className="hm-btn" type="button" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}

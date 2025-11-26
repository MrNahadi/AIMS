import React from 'react';
import ExplainabilityDisplay from './ExplainabilityDisplay';
import './ExplainabilityModal.css';

const ExplainabilityModal = ({ isOpen, onClose, shapValues }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content explainability-modal" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Feature Importance (SHAP Values)</h2>
                    <button className="modal-close-btn" onClick={onClose} aria-label="Close">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>
                <div className="modal-body">
                    <ExplainabilityDisplay shapValues={shapValues} />
                </div>
            </div>
        </div>
    );
};

export default ExplainabilityModal;

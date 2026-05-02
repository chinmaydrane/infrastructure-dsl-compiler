// Infrastructure DSL Playground - Frontend JavaScript

let editor;
let outputElement;
let compileBtn;
let clearBtn;
let copyBtn;
let loadingOverlay;
let errorModal;
let errorMessage;
let errorDetails;
let closeBtn;
let outputStatus;
let lineCount;
let charCount;

// Initialize Monaco Editor and UI
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    initializeMonacoEditor();
    setupEventListeners();
    updateEditorInfo();
});

function initializeElements() {
    // Get DOM elements
    outputElement = document.getElementById('output');
    compileBtn = document.getElementById('compileBtn');
    clearBtn = document.getElementById('clearBtn');
    copyBtn = document.getElementById('copyBtn');
    loadingOverlay = document.getElementById('loadingOverlay');
    errorModal = document.getElementById('errorModal');
    errorMessage = document.getElementById('errorMessage');
    errorDetails = document.getElementById('errorDetails');
    closeBtn = document.querySelector('.close');
    outputStatus = document.getElementById('outputStatus');
    lineCount = document.getElementById('lineCount');
    charCount = document.getElementById('charCount');
}

function initializeMonacoEditor() {
    // Configure Monaco Editor
    require.config({ paths: { 'vs': 'https://unpkg.com/monaco-editor@0.44.0/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        // Create editor
        editor = monaco.editor.create(document.getElementById('editor'), {
            value: `# Infrastructure DSL Example
# Write your DSL code here and click Compile

server "web_server" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu"
}

database "app_db" {
    engine = "mysql"
    storage = "100GB"
    version = "8.0"
}

network "vpc" {
    cidr_block = "10.0.0.0/16"
    public = true
}`,
            language: 'plaintext', // Use plaintext with custom syntax highlighting
            theme: 'vs',
            fontSize: 14,
            lineHeight: 1.4,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
            insertSpaces: true,
            rulers: [80],
            bracketPairColorization: { enabled: true },
            guides: {
                indentation: true,
                bracketPairs: true
            }
        });

        // Set up custom syntax highlighting for DSL
        setupDSLSyntaxHighlighting();

        // Listen for content changes
        editor.onDidChangeModelContent(updateEditorInfo);
    });
}

function setupDSLSyntaxHighlighting() {
    // Register DSL language
    monaco.languages.register({ id: 'infrastructure-dsl' });

    // Define language tokens
    monaco.languages.setMonarchTokensProvider('infrastructure-dsl', {
        tokenizer: {
            root: [
                // Comments
                [/#.*$/, 'comment'],
                
                // Resource types (keywords)
                [/\b(server|database|network|security_group|load_balancer|cache|container|function|subnet|module|variable|constant|role|policy|if|else|for|in|use|with|connect|attach|to|assign|user|group|param|return|true|false|null|and|or|not)\b/, 'keyword'],
                
                // Attribute names
                [/\b(cpu|memory|os|engine|version|storage|instance_class|cidr_block|enable_dns_hostnames|enable_dns_support|availability_zone|public|map_public_ip_on_launch|ingress|egress|from_port|to_port|protocol|security_groups|cidr_blocks|vpc|subnet_group|vpc_security_group_ids|node_type|num_cache_nodes|port|subnet_group_name|automatic_failover|multi_az_enabled|read_replica_count|multi_az|backup_window|maintenance_window|storage_type|storage_encrypted|parameters|tags|enabled|monitoring|algorithm|target_servers|listeners|certificate_arn|default_action|health_check|path|interval|timeout|healthy_threshold|unhealthy_threshold|metric|threshold|comparison|statistic|period|evaluation_periods|adjustment_type|scaling_adjustment|cold_storage_after_days|delete_after_days|lifecycle|backup_retention|scale_up_cooldown|scale_down_cooldown|log_groups|log_streams|min_instances|max_instances|desired_capacity)\b/, 'attribute.name'],
                
                // Strings
                [/"([^"\\]|\\.)*$/, 'string.invalid'],
                [/"/, 'string', '@string_double'],
                
                // Numbers
                [/\b\d+\.\d+/, 'number.float'],
                [/\b\d+/, 'number'],
                
                // Size units
                [/\b\d+(KB|MB|GB|TB)\b/, 'number'],
                
                // Operators
                [/[=<>!+\-*/%]/, 'operator'],
                
                // Punctuation
                [/[{}()\[\],;]/, 'delimiter'],
                
                // Identifiers
                [/\b[a-zA-Z_][a-zA-Z0-9_]*\b/, 'identifier'],
                
                // Whitespace
                [/[ \t\r\n]+/, 'white']
            ],
            
            string_double: [
                [/[^\\"]+/, 'string'],
                [/\\./, 'string.escape'],
                [/"/, 'string', '@pop']
            ]
        }
    });

    // Set language theme
    monaco.editor.setTheme('vs');
    
    // Apply DSL language to editor
    if (editor) {
        monaco.editor.setModelLanguage(editor.getModel(), 'infrastructure-dsl');
    }
}

function setupEventListeners() {
    // Compile button
    compileBtn.addEventListener('click', compileDSL);
    
    // Clear button
    clearBtn.addEventListener('click', clearEditor);
    
    // Copy button
    copyBtn.addEventListener('click', copyOutput);
    
    // Modal close button
    closeBtn.addEventListener('click', closeModal);
    
    // Close modal on outside click
    window.addEventListener('click', function(event) {
        if (event.target === errorModal) {
            closeModal();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl+Enter to compile
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();
            compileDSL();
        }
        // Escape to close modal
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

function updateEditorInfo() {
    if (!editor) return;
    
    const model = editor.getModel();
    const lineCountValue = model.getLineCount();
    const charCountValue = model.getValue().length;
    
    lineCount.textContent = `Lines: ${lineCountValue}`;
    charCount.textContent = `Chars: ${charCountValue}`;
}

async function compileDSL() {
    if (!editor) return;
    
    const dslCode = editor.getValue();
    
    if (!dslCode.trim()) {
        showError('Empty DSL Code', 'Please provide some DSL code to compile.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    clearOutput();
    
    try {
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: dslCode })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(result.output);
        } else {
            showError(result.error, result.details || [], result.phase);
        }
    } catch (error) {
        showError('Network Error', 'Failed to connect to the compiler server. Please make sure the server is running.');
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    compileBtn.disabled = loading;
    loadingOverlay.style.display = loading ? 'flex' : 'none';
    
    if (loading) {
        outputStatus.textContent = 'Compiling...';
        outputStatus.className = 'output-status loading';
    }
}

function clearOutput() {
    outputElement.textContent = '';
    outputElement.className = 'output-content';
    copyBtn.style.display = 'none';
    outputStatus.textContent = 'Ready';
    outputStatus.className = 'output-status';
}

function showSuccess(jsonOutput) {
    try {
        // Format JSON for display
        const formattedJson = JSON.stringify(JSON.parse(jsonOutput), null, 2);
        outputElement.textContent = formattedJson;
        outputElement.className = 'output-content';
        copyBtn.style.display = 'inline-block';
        outputStatus.textContent = 'Success';
        outputStatus.className = 'output-status success';
    } catch (error) {
        outputElement.textContent = jsonOutput;
        outputElement.className = 'output-content';
        copyBtn.style.display = 'inline-block';
        outputStatus.textContent = 'Success';
        outputStatus.className = 'output-status success';
    }
}

function showError(error, details = [], phase = 'error') {
    outputElement.textContent = `Error: ${error}`;
    outputElement.className = 'output-content error';
    copyBtn.style.display = 'none';
    outputStatus.textContent = 'Error';
    outputStatus.className = 'output-status error';
    
    // Show detailed error modal
    errorMessage.textContent = error;
    
    if (details && details.length > 0) {
        errorDetails.textContent = details.join('\n');
        errorDetails.style.display = 'block';
    } else {
        errorDetails.style.display = 'none';
    }
    
    errorModal.style.display = 'flex';
}

function closeModal() {
    errorModal.style.display = 'none';
}

function clearEditor() {
    if (editor) {
        editor.setValue('');
        editor.focus();
    }
    clearOutput();
}

async function copyOutput() {
    const outputText = outputElement.textContent;
    
    if (!outputText) return;
    
    try {
        await navigator.clipboard.writeText(outputText);
        
        // temporarily change button text to indicate success
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.backgroundColor = '#008000';
        copyBtn.style.color = 'white';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
            copyBtn.style.color = '';
        }, 2000);
    } catch (error) {
        console.error('Failed to copy text:', error);
    }
}

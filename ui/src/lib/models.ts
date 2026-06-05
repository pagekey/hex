// Copyright 2026 PageKey Solutions, LLC

export interface DataNode {
    id: string
    title: string
    value: string
    status: 'valid' | 'invalid' | 'pending'
}

export interface ProcessNode {
    id: string
    title: string
    code: string
    inputs: Record<string, string>
    outputs: Record<string, string>
    status: 'completed' | 'failed' | 'pending'
}

export interface Edge {
    start: string
    end: string
}

export interface Execution {
    id: string
    timestamp: string
    status: 'completed' | 'failed' | 'pending'
    dataNodes: DataNode[],
    processNodes: ProcessNode[],
    edges: Edge[],
}

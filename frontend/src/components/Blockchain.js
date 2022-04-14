import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import { API_BASE_URL } from '../config'
import Block from './Block';

const PAGE_RANGE = 3;

function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0)

    const fetchBlockchainPage = ({ start, end }) => {
        fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
            .then(r => r.json())
            .then(json => setBlockchain(json))
    }

    useEffect(() => {
        fetchBlockchainPage({ start: 0, end: PAGE_RANGE });
        fetch(`${API_BASE_URL}/blockchain/length`)
            .then(r => r.json())
            .then(json => setBlockchainLength(json))
    }, [])
    
    const buttonNumbers = []
    for (let i=0; i<Math.ceil(blockchainLength/PAGE_RANGE); i++) {
        buttonNumbers.push(i)
    }

    return (
        <div className="Blockchain">
            <h3>Blockchain</h3>
            <div>
                {
                    blockchain.map(block => <Block key={block.hash} block={block} />)
                }
            </div>
            <div>
                {
                    buttonNumbers.map(num => {
                        const start = num * PAGE_RANGE
                        const end = (num+1) * PAGE_RANGE
                        return (
                            <span key={num}>
                                <Button
                                    size="sm"
                                    onClick={() => fetchBlockchainPage({ start, end })}
                                >
                                    {num+1}
                                </Button>
                            </span>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Blockchain;
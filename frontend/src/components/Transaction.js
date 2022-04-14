import React from 'react';

function Transaction({ transaction }) {
    const { input, output } = transaction;
    const recipients = Object.keys(output);

    return (
        <div className="Transaction">
            <div>From: {input.address}</div>
            {
                recipients.map(recipient => (
                    <dib>
                        To: {recipient} - Sent: {output[recipient]}
                    </dib>
                ))
            }
        </div>
    )
}

export default Transaction;
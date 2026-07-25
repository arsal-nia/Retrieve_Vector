"use client";


import { useState } from "react";
import Sidebar from "@/components/Sidebar";

import ChatBox from "@/components/ChatBox";
import { ChatMessage, Conversation } from "@/lib/chat-types";

export default function Home() {
    const [collectionName, setCollectionName] = useState("");
    const initialConversation: Conversation = {
    id: crypto.randomUUID(),
    title: "New Chat",
    messages: [],
    createdAt: new Date(),
};

const [conversations, setConversations] = useState([
    initialConversation,
]);

const [currentConversationId, setCurrentConversationId] =
    useState(initialConversation.id);
    
const currentConversation =
    conversations.find(
        conversation =>
            conversation.id === currentConversationId
    )!;
   
    
    function updateCurrentConversationMessages(
    updater:
        | ChatMessage[]
        | ((previous: ChatMessage[]) => ChatMessage[])
) {
    setConversations(previous =>
        previous.map(conversation => {

            if (conversation.id !== currentConversationId) {
                return conversation;
            }

            const updatedMessages =
                typeof updater === "function"
                    ? updater(conversation.messages)
                    : updater;


            let updatedTitle = conversation.title;


            // Rename chat after first user message
            if (
                conversation.title === "New Chat" &&
                updatedMessages.length > 0
            ) {

                const firstUserMessage =
                    updatedMessages.find(
                        message =>
                            message.role === "user"
                    );


                if (firstUserMessage) {

                    updatedTitle =
                        firstUserMessage.content
                            .slice(0,30) + "...";

                }
            }


            return {
                ...conversation,

                title: updatedTitle,

                messages: updatedMessages,
            };
        })
    );
}

function createNewConversation() {
    const newConversation: Conversation = {
        id: crypto.randomUUID(),
        title: "New Chat",
        messages: [],
        createdAt: new Date(),
    };

    setConversations(previous => [
        newConversation,
        ...previous,
    ]);

    setCurrentConversationId(newConversation.id);
}

    return (
        <main className="app-shell">
            <Sidebar
    collectionName={collectionName}
    onUploadSuccess={setCollectionName}
    onNewChat={createNewConversation}
    conversations={conversations}
    currentConversationId={currentConversationId}
    onSelectConversation={setCurrentConversationId}
/>

            <section className="main-panel">

                

                

                {/* Chat */}
                <ChatBox
    collectionName={collectionName}
    messages={currentConversation.messages}
   setMessages={updateCurrentConversationMessages} 
/>

            </section>
        </main>
    );
}
import { createRxDatabase, addRxPlugin } from 'rxdb';
import { getRxStorageDexie } from 'rxdb/plugins/storage-dexie';

// Vamos armazenar a referência global do banco
let dbPromise = null;

const conversationSchema = {
    title: 'conversation schema',
    version: 0,
    primaryKey: 'id',
    type: 'object',
    properties: {
        id: { type: 'string', maxLength: 100 },
        title: { type: 'string' },
        createdAt: { type: 'number' }
    },
    required: ['id', 'title', 'createdAt']
};

const messageSchema = {
    title: 'message schema',
    version: 0,
    primaryKey: 'id',
    type: 'object',
    properties: {
        id: { type: 'string', maxLength: 100 },
        conversationId: { type: 'string', maxLength: 100 },
        role: { type: 'string' }, // 'user' ou 'assistant'
        content: { type: 'string' },
        createdAt: { type: 'number' }
    },
    required: ['id', 'conversationId', 'role', 'content', 'createdAt'],
    indexes: ['conversationId', 'createdAt']
};

export const initDB = async () => {
    if (dbPromise) return dbPromise;

    const createDB = async () => {
        const db = await createRxDatabase({
            name: 'catequistadb',
            storage: getRxStorageDexie()
        });

        await db.addCollections({
            conversations: {
                schema: conversationSchema
            },
            messages: {
                schema: messageSchema
            }
        });

        return db;
    };

    dbPromise = createDB();
    return dbPromise;
};

export const getDB = async () => {
    if (!dbPromise) {
        return await initDB();
    }
    return dbPromise;
};

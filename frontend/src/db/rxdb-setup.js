import { createRxDatabase, addRxPlugin } from 'rxdb';
import { getRxStorageDexie } from 'rxdb/plugins/storage-dexie';
import { RxDBMigrationSchemaPlugin } from 'rxdb/plugins/migration-schema';
import { RxDBQueryBuilderPlugin } from 'rxdb/plugins/query-builder';

addRxPlugin(RxDBMigrationSchemaPlugin);
addRxPlugin(RxDBQueryBuilderPlugin);

// Vamos armazenar a referência global do banco
let dbPromise = null;

const conversationSchema = {
    title: 'conversation schema',
    version: 2,
    primaryKey: 'id',
    type: 'object',
    properties: {
        id: { type: 'string', maxLength: 100 },
        title: { type: 'string' },
        createdAt: { type: 'number' },
        pinned: { type: 'boolean' }
    },
    required: ['id', 'title', 'createdAt'],
    indexes: ['createdAt']
};

const messageSchema = {
    title: 'message schema',
    version: 1,
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
                schema: conversationSchema,
                migrationStrategies: { 
                    1: (oldDoc) => oldDoc,
                    2: (oldDoc) => {
                        oldDoc.pinned = false;
                        return oldDoc;
                    }
                }
            },
            messages: {
                schema: messageSchema,
                migrationStrategies: { 1: (oldDoc) => oldDoc }
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

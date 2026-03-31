import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { PostService } from '../PostService';
import { describe, it, expect } from 'vitest';
import * as path from 'path';
import type { CreatePostDto } from '../types';

const { integer, string } = MatchersV3;

const provider = new PactV3({
    consumer: 'FrontendConsumer',
    provider: 'BackendProvider',
    dir: path.resolve(process.cwd(), '../pacts'),
});

describe('PostService Pact - Get Post by ID', () => {
    it('returns a post by id', async () => {
        provider.addInteraction({
            states: [{ description: 'post with id 1 exists' }],
            uponReceiving: 'a request for post by id',
            withRequest: {
                method: 'GET',
                path: '/posts/1/',
            },
            willRespondWith: {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    success: true,
                    data: {
                        id: integer(1),
                        title: string('Pact Title'),
                        content: string('Pact Content'),
                        userId: integer(2),
                        created_at: string('2024-01-01T00:00:00Z'),
                        updated_at: string('2024-01-01T00:00:00Z'),
                    },
                },
            },
        });

        await provider.executeTest(async (mockServer) => {
            const postService = new PostService(mockServer.url);
            const response = await postService.getPostById(1);
            expect(response.success).toBe(true);
            expect(response.data?.id).toBe(1);
            expect(response.data?.title).toBe('Pact Title');
        });
    });
});

describe('PostService Pact - Create Post', () => {
    it('creates a new post', async () => {
        const newPost: CreatePostDto = {
            title: 'New Post',
            content: 'New Content',
            user_id: 2,
        };

        provider.addInteraction({
            states: [{ description: 'user with id 2 exists' }],
            uponReceiving: 'a request to create a post',
            withRequest: {
                method: 'POST',
                path: '/posts/',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: newPost,
            },
            willRespondWith: {
                status: 201,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    success: true,
                    message: string('Post created successfully'),
                },
            },
        });

        await provider.executeTest(async (mockServer) => {
            const postService = new PostService(mockServer.url);
            const response = await postService.createPost(newPost);
            expect(response.success).toBe(true);
            expect(response.message).toBe('Post created successfully');
        });
    });
});

import { useState } from 'react';
import { PostService } from '../api/PostService';
import type { CreatePostDto } from '../api/types';

interface CreatePostProps {
  onSuccess: () => void;
  token: string | null;
  userId: number;
}

const API_URL = 'http://localhost:8000';

export function CreatePost({ onSuccess, token, userId }: CreatePostProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      setError('You must be logged in to create a post');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const service = new PostService(API_URL);
      const newPost: CreatePostDto = {
        title,
        content,
        user_id: userId,
      };
      
      const response = await service.createPost(newPost);
      if (response.success) {
        setSuccess(true);
        setTimeout(() => {
          onSuccess();
        }, 1500);
      } else {
        setError(response.message || 'Failed to create post');
      }
    } catch (err) {
      setError('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="success-message">
        <h2>✅ Post Created!</h2>
        <p>Redirecting to posts...</p>
      </div>
    );
  }

  return (
    <div className="create-post">
      <h2>Create New Post</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            placeholder="Enter post title"
          />
        </div>
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows={10}
            placeholder="Write your post content here..."
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Post'}
        </button>
      </form>
    </div>
  );
}

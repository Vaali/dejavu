# Changes

## 1.3

### 1.3.4
* added `CHANGES.md` for update tracking
* modified database schema (**BREAKING CHANGE**) for faster indexing (use `base64`, not `binary`, add index)
* removed redundant `file_hash` compute from within fingerprinting loop
* avoid loading all hashes from database for reindexing check, use one-off query
* add default [sqlite](https://sqlite.org/) database for testing if `DATABASE_URL` not set


# BullMQ4168 independent final matrix

Final source: `2e5ecf53615fd799d0c660d3b8bb8a5af579ccf7`; tree `0503ca913f5b3b71b081f7912a497fe635317d67`.
Frozen archive SHA256: `7bc67762360cab5ec31cc6f42e95cbc9c8d2401364a40b5129cf5bf2e10193a3`.

All1068 archived paths, Git blob IDs, bytes, executable modes and symlink targets match the committed host tree. Each runtime tree passes a full1068-path check before and after its final tests. Exact commands, process exit codes, log hashes and unchanged skip IDs are recorded in `v2-final-gates.json`.

| Runtime / real store | Official command | Passed files / tests | Existing skips | Exit |
|---|---|---:|---:|---:|
| v20.20.2 / Redis7.4.11 | `yarn test` | 49 / 1114 | 3 | 0 |
| v20.20.2 / Redis7.4.11 | `yarn test:ioredis` | 6 / 206 | 11 | 0 |
| v22.23.4 / Redis7.4.11 | `yarn test` | 49 / 1114 | 3 | 0 |
| v22.23.4 / Redis7.4.11 | `yarn test:ioredis` | 6 / 206 | 11 | 0 |
| v24.22.1 / Valkey8.0.1 (redis_version compatibility7.2.4) | `yarn test:valkey-glide` | 48 / 1093 | 3 | 0 |

All lanes ran a successful complete `yarn build`. Yarn1.22.22 installs used `yarn install --ignore-engines --frozen-lockfile --non-interactive`. Node22 reused its already completed frozen install; neither package.json nor yarn.lock changed in the formatting-only source update. Node20 and the GLIDE lane installed independently. Target Node20.20.2/22.23.4/24.22.1 binaries are asserted in the logs; the container base image carries Node26, which is not the Node interpreter used for these gates. npm11.20.0, Debian12 and the actual Linux kernel are retained in version logs.

The GLIDE lane follows the separate upstream workflow: `npm install --no-save @valkey/valkey-glide@2.5.0`, then `yarn build` and `yarn test:valkey-glide`. GLIDE2.5.0 was asserted and exercised through its real native adapter against a dedicated Valkey8.0.1 instance. Its compatibility redis_version is7.2.4; the two Redis lanes use Redis7.4.11.

The official extra npm install rewrote yarn.lock. The first full GLIDE suite passed, but its source postcheck correctly failed on that lock drift. The mutated lock and diff were retained. Only the isolated validation tree was restored to the exact committed lock bytes after installation; the installed native adapter remained unchanged. Build, the complete GLIDE suite and full source checks were rerun successfully. Use the `v2-glide-canonical-final-*` logs for the final result; the earlier GLIDE pass does not stand in for this rerun. See `v2-glide-lock-side-effect.json`.

The three lanes use different worker containers and different real store containers, with no published host ports. Each worker shares only its own store network namespace, so localhost:6379 cannot target another project. Exact names, IDs, image IDs, labels and network modes are in the fixed `v2-runtime-identities.json` snapshot. No source edits, commits, GitHub requests, paid services or model calls were made by this matrix worker. This proves the assigned local CI commands, not hosted GitHub Actions or paid-provider acceptance.

Historical v1, interrupted v1 Node22, initial missing-Yarn setup failure, the tmpfs Docker-copy failure, and the first GLIDE lock-drift postcheck are retained locally. They are not counted as final passes. Initial pre/post-restart read-only inspect calls reused filenames; those historical rows are excluded from canonical public proof in favor of the fresh fixed identity snapshot. Normal commit hooks were performed by the coordinating worker, not by these archive-only runtime trees.

The explicit public file allowlist is `public-allowlist.json`; other files and caches are local execution history. All test skip IDs and original logs remain available for review.

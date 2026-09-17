## 2026-09-17 – Open API exposure (anonymous access)

- Anonymous `GET /recipes` returned all recipes with status 200, including `"is_public": false` items like "Secret family hot sauce" (id 3). Any requester can read all recipe data.
- Anonymous `PATCH /recipes/1` with `{"title": "Hacked Shakshuka"}` returned 200 and updated the stored recipe. Any requester can modify existing recipes.
- Anonymous `DELETE /recipes/2` returned 204, and a follow-up `GET /recipes/2` returned 404 "recipe not found". Any requester can delete recipes.
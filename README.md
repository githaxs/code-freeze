# Code Freeze

> Block merges during configurable code freezes

### Installation
To Install globally:

```yaml
# githaxs_settings/ghx.yml

code-freeze:
  # install on all repos
  org: true
  org_settings:
    # Final settings cannot be overriden by repo specific settings
    final:
      block_times:
        - "* * * * 6,0"
    # Default value if final and repo specific settings do not exist
    default:
      block_times:
        - "* * * * 6,0"
  # install on select repos
  repos:
    - api-microservice
    - website
```

### Configuration
|parameter|description|required|default|
|---|---|---|---|
|block_times| A **list** of times when pull requests should not be merged. The times follow standard CRON syntax and can be test at [crontab.pro](https://crontab.pro/). See `src/test_task.py` for example configurations and tests. | no | 0 |

### Example Configuration
```yaml
# <repo name>/ghx.yml

code-freeze:
  repo_settings:
    block_times:
    # Block merges on Saturday and Sunday
      - "* * * * 6,0"
```

### Actions
|name|description|
|---|---|
|override| Manually override a failing check. The task will post a comment on GitHub indicating which user has overridden the result.|

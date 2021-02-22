# Code Freeze

> Block merges during configurable code freezes

### Global Installation and Settings
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

### Local Installation and Settings

To configure repo specific settings:
```yaml
# api-microservice/ghx.yml

code-freeze:
  repo_settings:
    block_times:
      - "* * * * 6,0"
```

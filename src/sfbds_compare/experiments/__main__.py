"""Run experiments from YAML.

  python -m sfbds_compare.experiments --config path/to.yaml
  python -m sfbds_compare.experiments --config-dir path/to/dir
"""

from sfbds_compare.experiments.runner import main

raise SystemExit(main())

$: syndicate generate project --name syndicate-quickstart-project
$: syndicate generate config --name "dev" ...
$: syndicate generate lambda --name api_handler --runtime python

(syndicate_venv) ➜  syndicate-quickstart-project tree
.
├── CHANGELOG.md
├── deployment_resources.json
├── README.md
├── src
│   ├── commons
│   │   ├── abstract_lambda.py
│   │   ├── exception.py
│   │   ├── __init__.py
│   │   └── log_helper.py
│   └── lambdas
│       ├── api_handler
│       │   ├── deployment_resources.json
│       │   ├── handler.py
│       │   ├── __init__.py
│       │   ├── lambda_config.json
│       │   ├── local_requirements.txt
│       │   └── requirements.txt
│       └── __init__.py
└── tests
    ├── __init__.py
    └── test_api_handler
        ├── __init__.py
        └── test_success.py

$: syndicate generate lambda_layer --name weather --runtime python --link_with_lambda api_handler
$: syndicate_venv) ➜  syndicate-quickstart-project tree
.
├── CHANGELOG.md
├── deployment_resources.json
├── README.md
├── src
│   ├── commons
│   │   ├── abstract_lambda.py
│   │   ├── exception.py
│   │   ├── __init__.py
│   │   └── log_helper.py
│   └── lambdas
│       ├── api_handler
│       │   ├── deployment_resources.json
│       │   ├── handler.py
│       │   ├── __init__.py
│       │   ├── lambda_config.json
│       │   ├── local_requirements.txt
│       │   └── requirements.txt
│       ├── __init__.py
│       └── layers
│           └── weather
│               ├── lambda_layer_config.json
│               ├── local_requirements.txt
│               └── requirements.txt
└── tests
    ├── __init__.py
    └── test_api_handler
        ├── __init__.py
        └── test_success.py

then add weather.py, modify requirements.txt

(syndicate_venv) ➜  syndicate-quickstart-project tree
.
├── CHANGELOG.md
├── deployment_resources.json
├── README.md
├── src
│   ├── commons
│   │   ├── abstract_lambda.py
│   │   ├── exception.py
│   │   ├── __init__.py
│   │   └── log_helper.py
│   └── lambdas
│       ├── api_handler
│       │   ├── deployment_resources.json
│       │   ├── handler.py
│       │   ├── __init__.py
│       │   ├── lambda_config.json
│       │   ├── local_requirements.txt
│       │   └── requirements.txt
│       ├── __init__.py
│       └── layers
│           └── weather
│               ├── lambda_layer_config.json
│               ├── local_requirements.txt
│               ├── requirements.txt
│               └── weather.py
└── tests
    ├── __init__.py
    └── test_api_handler
        ├── __init__.py
        └── test_success.py


$: syndicate build
$: syndicate deploy


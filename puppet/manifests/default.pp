class {'::mongodb::globals':
  manage_package_repo => true,
}->
class {'::mongodb::server':
  bind_ip => ['0.0.0.0']
}

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# TODO - Remove implementation of MonkeyPatching ToJsonString once issue
# has been addressed in the protobuf library.
def patch_to_json_method(obj):
    """Monkey patches an object's ToJsonString method.

    Args:
        obj: An arbitrary object.isinstance
    """
    obj.ToJsonString = _patched_to_json_string


def _patched_to_json_string(self):
    """Converts an objects paths array to a camel cased string."""
    try:
        iter(self.paths)
    except TypeError:
        paths = []
    else:
        paths = self.paths

    camelcase_paths = []

    for path in paths:
        camelcase_paths.append(_snake_case_to_camel_case(path))

    return ','.join(camelcase_paths)


def _snake_case_to_camel_case(path_name):
  """Converts a path name from snake_case to camelCase.

  This is a slightly modified version of the function defined in the protobuf
  library here: https://github.com/protocolbuffers/protobuf/blob/master/python/google/protobuf/internal/well_known_types.py#L506
  """
  result = []
  after_underscore = False
  for c in path_name:
    if c.isupper():
      raise Error('Fail to print FieldMask to Json string: Path name '
                  '{0} must not contain uppercase letters.'.format(path_name))
    if after_underscore:
      if c.islower() or c.isdigit():
        result.append(c.upper())
        after_underscore = False
      else:
        raise Error('Fail to print FieldMask to Json string: The '
                    'character after a "_" must be a lowercase letter '
                    'in path name {0}.'.format(path_name))
    elif c == '_':
      after_underscore = True
    else:
      result += c

  if after_underscore:
    raise Error('Fail to print FieldMask to Json string: Trailing "_" '
                'in path name {0}.'.format(path_name))
  return ''.join(result)


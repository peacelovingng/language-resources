# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Various helper functions."""

import io

import six
from google.protobuf import text_format


def GetTextProto(filename, message):
  with io.open(filename, 'rb') as stream:
    data = stream.read()
  return ParseFromBytes(data, message)


def ParseFromBytes(data, message):
  if six.PY3:
    # Appalling but apparently necessary hack to work around protobuf.
    data = data.decode('latin-1').encode('utf-8')  # NEVER TRY THIS AT HOME!
  message.Clear()
  return text_format.Parse(data, message)


def SetTextProto(filename, message):
  SetTextContents(filename, MessageToUnicodeString(message))
  return


def SetTextContents(filename, contents):
  assert isinstance(contents, six.text_type)
  with io.open(filename, mode='wt', encoding='utf-8') as writer:
    writer.write(contents)
  return


def MessageToUnicodeString(message, **kwargs):
  kwargs['as_utf8'] = True
  text = text_format.MessageToString(message, **kwargs)
  if six.PY3:
    # Appalling but apparently necessary hack to work around protobuf.
    text = text.encode('latin-1')  # NEVER TRY THIS AT HOME!
  text = text.decode('utf-8')
  return text


def EnsureUnicode(bytes_or_string):
  if isinstance(bytes_or_string, six.binary_type):
    return bytes_or_string.decode('utf-8')
  else:
    assert isinstance(bytes_or_string, six.text_type)
    return bytes_or_string